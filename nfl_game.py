import os
import pandas as pd

base = "data"


class Play:
    def __init__(self, details, player_tracking, pff):
        self.details = details
        self.player_tracking = player_tracking
        self.pff = pff
        self.frames = list(self.player_tracking["frameId"].unique())

    def get_frame(self, frameId):
        frame_player_tracking = self.player_tracking[
            self.player_tracking["frameId"] == frameId
        ]
        return frame_player_tracking


class Game:
    def __init__(self, gameId):
        self.load_game_data(gameId)
        self.play_ids = list(self.player_tracking["playId"].unique())

    def load_game_data(self, gameId):

        games_df = pd.read_csv(os.sep.join([base, "games.csv"]))
        self.details = games_df[games_df["gameId"] == gameId].iloc[0, :].to_dict()

        player_tracking = pd.read_csv(
            os.sep.join([base, f"week{self.details['week']}.csv"])
        )
        self.player_tracking = player_tracking[player_tracking["gameId"] == gameId]

        pff = pd.read_csv(os.sep.join([base, "pffScoutingData.csv"]))
        self.pff = pff[pff["gameId"] == gameId]

        plays = pd.read_csv(os.sep.join([base, "plays.csv"]))
        self.play_data = plays[plays["gameId"] == gameId]

    def get_play(self, playId):
        play_tracking_data = self.player_tracking[
            self.player_tracking["playId"] == playId
        ]
        play_pff_data = self.pff[self.pff["playId"] == playId]
        play_details = (
            self.play_data[self.play_data["playId"] == playId].iloc[0, :].to_dict()
        )

        return Play(play_details, play_tracking_data, play_pff_data)
