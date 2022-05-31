<template>
  <div>
    <h1>Quiz page</h1>
    <div id="name-form">
      <p>Saisissez votre nom</p>
      <input type="text" placeholder="Username" v-model="username" />
    </div>
    <button class="btn btn-primary" @click="launchNewQuiz">Ok</button>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "NewQuizPage",
  data() {
    return {
      username: ""
    }
  },
  methods: {
    launchNewQuiz() {
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
    }
  }
};
</script>