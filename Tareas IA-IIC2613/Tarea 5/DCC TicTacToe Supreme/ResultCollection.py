# NO TOCAR
import csv


class ResultCollection:
    results = []

    @staticmethod
    def add_result(winner, avg_player1, avg_player2, depth1, depth2,
                   use_alphabeta1, use_alphabeta2, evaluation1, evaluation2,
                   total_player1, total_player2):
        ResultCollection.results.append({
            "WINNER": winner,
            "AVG_TIME_PLAYER_1": avg_player1,
            "AVG_TIME_PLAYER_2": avg_player2,
            "DEPTH_PLAYER_1": depth1,
            "DEPTH_PLAYER_2": depth2,
            "USE_ALPHABETA_PLAYER_1": use_alphabeta1,
            "USE_ALPHABETA_PLAYER_2": use_alphabeta2,
            "EVALUATION_FUNCTION_PLAYER_1": evaluation1,
            "EVALUATION_FUNCTION_PLAYER_2": evaluation2,
            "TOTAL_TIME_PLAYER_1": total_player1,
            "TOTAL_TIME_PLAYER_2": total_player2,
        })

    @staticmethod
    def get_results():
        return ResultCollection.results.copy()

    @staticmethod
    def export_to_csv(filename):
        if not ResultCollection.results:
            return
        keys = ResultCollection.results[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(ResultCollection.results)

    @staticmethod
    def clear_results():
        ResultCollection.results = []
