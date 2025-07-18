########################################################################################################
###############################        EVALUADOR RUBRICA GEMINI        #################################
########################################################################################################
# CONSTRUCCION DEL PROMPT, EJEMPLOS DE TURNOS EVALUADOS Y TURNOS A EVALUAR - GEMINI-2.0-FLASH 

import pandas as pd
import json
import time
import requests

API_KEY = "APIKEY"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def cargar_csv_como_texto(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()

def construir_prompt_batch(turnos_batch, ejemplos_csv_texto):
    instrucciones = (
        "You are an expert evaluator of the Tic-Tac-Toe game. Your task is to analyze each move based on two main aspects:\n\n"
        "1. Apply a rubric with 7 dimensions to evaluate the quality of the move proposed by a language model.\n"
        "2. Determine the current game state based exclusively on the current board and the move made.\n\n"

        "=== Game Rules (Tic-Tac-Toe) ===\n"
        "- Two players: 'x' always starts first, followed by 'o'.\n"
        "- The board is a 3x3 grid. An empty cell is represented by 'b'.\n"
        "- A player wins by placing three of their symbols (x or o) in a line: horizontal, vertical, or diagonal.\n"
        "- Winning combinations include:\n"
        "  • Horizontals: (1,1)-(1,2)-(1,3), (2,1)-(2,2)-(2,3), (3,1)-(3,2)-(3,3)\n"
        "  • Verticals: (1,1)-(2,1)-(3,1), (1,2)-(2,2)-(3,2), (1,3)-(2,3)-(3,3)\n"
        "  • Diagonals: (1,1)-(2,2)-(3,3) and (1,3)-(2,2)-(3,1)\n"
        "- Players alternate turns. A player cannot play twice in a row.\n"
        "- Moves are represented as: [\"mark\", row, column]\n"
        "- The board state provided with each move already includes the cell marked by the current player.\n\n"

        "=== Game State Evaluation (field \"estado\") ===\n"
        "Assign one of the following states per move, based solely on the board:\n"
        "• \"victoria\": if the current player has formed three in a row in this move.\n"
        "• \"derrota\": assigned only after the opponent has won (i.e., after a turn with win=1 from the rival).\n"
        "• \"empate\": if the board is full (9 marked cells) and no player has won.\n"
        "• \"en partida\": if the game continues (there are empty cells and no winner yet).\n"
        "• \"invalido\": if the move is illegal, e.g.,\n"
        "   - marking a previously occupied cell,\n"
        "   - playing out of turn (same player twice in a row),\n"
        "   - the move does not correspond to the newly marked cell on the board,\n"
        "   - the move format is incorrect.\n\n"
        "Additional rules:\n"
        "- Only one player per game can receive \"victory\" and one \"defeat\".\n"
        "- \"defeat\" must never be assigned before a valid \"victory\".\n"
        "- Assign \"invalid\" if any serious rule violation occurs.\n\n"

        "=== Evaluation Rubric Instructions ===\n"
        "Rate each dimension from 1 to 3, using these exact descriptions:\n\n"

        "1. Comprensión de Reglas:\n"
        "  - 1 (Deficient): Violates basic rules: occupied cell or outside the board.\n"
        "  - 2 (Acceptable): Fulfills basic rules but misses less obvious situations.\n"
        "  - 3 (Optimal): Always legal moves, fully respecting turn rules.\n\n"

        "2. Validez y Legalidad:\n"
        "  - 1 (Deficient): Invalid or illegal move (out of bounds).\n"
        "  - 2 (Acceptable): Valid move without deep analysis.\n"
        "  - 3 (Optimal): Valid move chosen after full board analysis.\n\n"

        "3. Razonamiento Estratégico:\n"
        "  - 1 (Deficient): Illogical, random or counterproductive action.\n"
        "  - 2 (Acceptable): Simple strategic intent (block/advance), no anticipation.\n"
        "  - 3 (Optimal): Clear, anticipatory justification maximizing winning chances.\n\n"

        "4. Factualidad:\n"
        "  - 1 (Deficient): Explanation incorrect or unrelated to the real board.\n"
        "  - 2 (Acceptable): Generally correct justification with minor inaccuracies.\n"
        "  - 3 (Optimal): Precise explanation based on concrete facts of the board.\n\n"

        "5. Coherencia Explicativa:\n"
        "  - 1 (Deficient): Confusing or contradictory explanation.\n"
        "  - 2 (Acceptable): Clear but superficial explanation.\n"
        "  - 3 (Optimal): Logical, complete explanation aligned with the move.\n\n"

        "6. Claridad Lingüística:\n"
        "  - 1 (Deficient): Unclear language or major errors.\n"
        "  - 2 (Acceptable): Clear language with minor errors.\n"
        "  - 3 (Optimal): Precise, grammatically correct, and easy to understand.\n\n"

        "7. Adaptabilidad:\n"
        "  - 1 (Deficient): Ignores opponent’s previous moves.\n"
        "  - 2 (Acceptable): Basic or delayed adaptation.\n"
        "  - 3 (Optimal): Quickly adapts and adjusts strategy effectively.\n\n"

        "=== Key Considerations ===\n"
        "- The 'board' field already reflects the current move.\n"
        "- Do not mark a move invalid just because the cell is occupied (it may have been marked this turn).\n"
        "- A move is valid if it exactly matches the newly marked cell for that player on the current board.\n"
        "- The first move (turn 1) should always be considered valid unless the 'move' field is missing, malformed, or does not follow the expected format.\n"
        "- Evaluate the game state ignoring the textual explanation.\n\n"


        "=== Output Format (Output Must Be in Spanish) ===\n"
        "You must return only a plain CSV table (no JSON, no markdown, no extra text), with one row per evaluated move, in the same order as provided.\n"
        "Each row must contain the following fields, in this exact order:\n"
        "- \"id_match\": Match identifier\n"
        "- \"modelo\": Name of the model that made the move\n"
        "- \"jugador\": Player symbol ('x' or 'o')\n"
        "- \"estado\": One of the following values (in Spanish): \"victoria\", \"derrota\", \"empate\", \"en partida\", \"invalido\"\n"
        "- \"rubrica\": A JSON-like object (in text format) with 7 dimensions as keys and integer values from 1 to 3 — the object must be serialized as a valid string within the CSV row (use double quotes escaped as \"\")\n"
        "- \"explicacion\": A JSON-like object (in text format) with 7 keys, each containing a short explanation of the assigned score — also serialized as a valid string within the CSV row\n\n"
        "- \"timestamp\": Date of the move\n"
        "- \"execution_time\": execution time of turn\n"
        "Example of correct output format:\n"
        "id_match,modelo,jugador,estado,rubrica,explicacion,timestamp,execution_time\n"
        "Example: id_match,modelo,jugador,en partida,\"{Comprensión de Reglas: nota, ..... , Adaptabilidad: nota}\",\"{Comprensión de Reglas: nota - reason.,.....,Adaptabilidad: nota - reason.}\", 2025-03-07T01:58:35.398Z, 1.652608499978669\n\n"
        "DO NOT return JSON arrays, markdown tables, or explanations outside of the CSV.\n"
        "Return only a raw CSV with values in Spanish, properly escaped and quoted, suitable for programmatic parsing.\n\n"
        "Now evaluate the following moves:"
    )

    turnos_texto = ""
    for idx, (_, turno) in enumerate(turnos_batch.iterrows(), start=1):
        turno_json = turno.to_json(force_ascii=False)
        turnos_texto += f"\n--- Turno {idx} ---\n{turno_json}"

    prompt = instrucciones + "\n" + ejemplos_csv_texto + "\n" + turnos_texto + "\n\nReturn only a plain CSV output. Include the header row (id_partida,modelo,jugador,estado,rubrica,explicacion,timestamp) only once at the beginning of the first batch. For all subsequent batches, omit the header and return only the rows. Do not wrap the CSV output in code blocks like ```csv or ```."
    return prompt

def post_con_reintentos(prompt, max_retries=5, initial_backoff=1.0):
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    backoff = initial_backoff
    for attempt in range(1, max_retries + 1):
        response = requests.post(
            API_URL,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload)
        )
        if response.status_code == 429:
            print(f"Rate limit (429). Esperando {backoff}s antes de reintentar ({attempt}/{max_retries})...")
            time.sleep(backoff)
            backoff *= 2
            continue
        if response.status_code != 200:
            print("Error en la respuesta:", response.status_code, response.text)
            break
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

    raise Exception(f"No se pudo completar tras {max_retries} reintentos.")

def evaluar_csv(csv_path, ejemplos_path, salida_csv, batch_size=5):
    ejemplos_csv_texto = cargar_csv_como_texto(ejemplos_path)

    df_turnos = pd.read_csv(csv_path)

    resultados = []

    for start_idx in range(0, len(df_turnos), batch_size):
        batch = df_turnos.iloc[start_idx:start_idx + batch_size]

        prompt = construir_prompt_batch(batch, ejemplos_csv_texto)

        print(f"Procesando batch desde índice {start_idx}...")

        respuesta = post_con_reintentos(prompt)

        resultados.append(respuesta)

    lineas = []
    for i, texto in enumerate(resultados):
        lineas_batch = texto.strip().splitlines()
        if i > 0:
            lineas_batch = lineas_batch[1:]
        lineas.extend(lineas_batch)
    with open(salida_csv, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"Evaluación completada. Resultados guardados en {salida_csv}")

if __name__ == "__main__":
    csv_turnos =   r"\dataset1.csv"
    csv_ejemplos = r"\ejemplo.csv"
    salida =       r"\evaluadoGemini.csv"

    evaluar_csv(csv_turnos, csv_ejemplos, salida, batch_size=20)