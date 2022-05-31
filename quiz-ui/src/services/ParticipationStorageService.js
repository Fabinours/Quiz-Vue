
const PLAYER_NAME_KEY = 'playerName';
const PLAYER_SCORE_KEY = 'playerScore';

export default {
  clear() {
    window.localStorage.clear();
  },
  savePlayerName(playerName) {
    window.localStorage.setItem(PLAYER_NAME_KEY, playerName);
  },
  getPlayerName() {
    return window.localStorage.getItem(PLAYER_NAME_KEY);
  },
  saveParticipationScore(participationScore) {
    window.localStorage.setItem(PLAYER_SCORE_KEY, participationScore);
  },
  getParticipationScore() {
    return window.localStorage.getItem(PLAYER_SCORE_KEY);
  }
};