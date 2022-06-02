
const PLAYER_NAME_KEY = 'playerName';
const PLAYER_SCORE_KEY = 'playerScore';
const TOKEN_KEY = 'token';
const ERROR_KEY = 'error';

// Enregistrement de certaines variables dans le localStorage
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
  },
  saveToken(token) {
    window.localStorage.setItem(TOKEN_KEY, token);
  },
  removeToken() {
    window.localStorage.removeItem(TOKEN_KEY);
  },
  getToken() {
    let token = window.localStorage.getItem(TOKEN_KEY);
    return token ? token : null;
  },
  getError() {
    let error = window.localStorage.getItem(ERROR_KEY);
    return error ? error : null;
  },
  setError(error) {
    window.localStorage.setItem(ERROR_KEY, error);
  }
};