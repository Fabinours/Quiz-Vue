import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
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
        console.error(error);
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  login() {
    return this.call("post", "login");
  },
  getQuestion(position) {
    return this.call("get", `questions/${position}`);
  },
  getAllQuestions() {
    return this.call("get", "questions");
  },
  createQuestion() {
    return this.call("post", "questions");
  },
  updateQuestion(position) {
    return this.call("put", `questions/${position}`);
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