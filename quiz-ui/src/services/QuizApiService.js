import axios from "axios";
import router from '../router'
import ParticipationStorageService from "./ParticipationStorageService";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  // Appel à l'API et vérification du token
  async call(method, resource, data = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    const token = ParticipationStorageService.getToken();

    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        ParticipationStorageService.setError("Une erreur est survenue lors de la connexion au serveur");
        router.push('/error');
        return { status: error.response.status, data: error.response.statusText };
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  login(password) {
    return this.call("post", "login", password);
  },
  getQuestion(position) {
    return this.call("get", `questions/${position}`);
  },
  getAllQuestions() {
    return this.call("get", "questions");
  },
  createQuestion(question) {
    return this.call("post", "questions", question);
  },
  updateQuestion(position, question) {
    return this.call("put", `questions/${position}`, question);
  },
  deleteQuestion(position) {
    return this.call("delete", `questions/${position}`);
  },
  createParticipation(participation) {
    return this.call("post", "participations", participation);
  },
  deleteAllParticipations() {
    return this.call("delete", "participations");
  }
};