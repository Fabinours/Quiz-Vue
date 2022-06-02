<template>
  <div class="d-flex justify-content-center">
    <div class="card mx-3" style="width: 20rem;">
      <div class="card-body mt-2">
        <h2 class="card-title">Votre pseudo ? ✌</h2>
        <div id="name-form">
          <label for="username">Saisissez votre nom</label>
          <input id="username" class="form-control mt-2" type="text" placeholder="Pseudo" v-model="username" />
        </div>
      </div>
      <div class="card-body d-flex justify-content-center">
        <RouterLink to="/questions">
          <button class="btn btn-primary" @click="launchNewQuiz">
            Démarrer le quiz
          </button>
        </RouterLink>
      </div>
    </div>
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
      //Enregistrement du pseudo du participant et place au jeu
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
    }
  }
};
</script>