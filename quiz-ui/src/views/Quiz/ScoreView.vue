<template>
  <div class="d-flex justify-content-center">
    <div class="card mx-3" style="width: 20rem;">
      <div class="card-body">
        <h2 class="card-title">Mon score 😊</h2>
        <p class="card-text">
          Félicitations, vous avez obtenu un score de {{ currentScore }} ! Vous êtes à la {{ playerPodium }}ème place !
        </p>
      </div>

      <ul class="list-group list-group-flush">
        <li class="list-group-item" v-for="({ playerName, score }, i) in nearToUserRegisteredScores" :key="i">
          {{ nearToUserRegisteredScoresMinPodium + i }}/{{ parcipationNb }} : {{ playerName }} - {{ score }}
        </li>
      </ul>
    </div>

    <div class="card mx-3" style="width: 20rem;">
      <div class="card-body">
        <h2 class="card-title">Meilleurs scores 👌</h2>
      </div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item" v-for="({ playerName, score }, i) in registeredScores" :key="i">
          {{ i + 1 }}/{{ parcipationNb }} : {{ playerName }} avec {{ score }} points !
        </li>
      </ul>

      <div class="card-body d-flex justify-content-center">
        <RouterLink to="/quiz">
          <button class="btn btn-primary">
            Rejouer
          </button>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "HomePage",
  async created() {
    const currentScore = participationStorageService.getParticipationScore()
    const currentPlayerName = participationStorageService.getPlayerName()

    const response = await quizApiService.getQuizInfo();
    const index = response.data.scores.findIndex(({ playerName, score}) => playerName === currentPlayerName && score == currentScore);
    const minIndex = Math.max(0, index - this.nearToUserRegisteredScoresRange);
    const maxIndex = Math.min(response.data.scores.length, index + this.nearToUserRegisteredScoresRange + 1);
    
    this.currentScore = currentScore;
    this.playerPodium = index + 1;
    this.nearToUserRegisteredScoresMinPodium = minIndex + 1;
    this.nearToUserRegisteredScores = response.data.scores.slice(minIndex, maxIndex);
    this.registeredScores = response.data.scores.slice(0, this.registeredScoresSize);
    this.parcipationNb = response.data.scores.length;
  },
  data() {
    return {
      currentScore: 0,

      nearToUserRegisteredScoresRange: 2,
      playerPodium: 0,
      nearToUserRegisteredScoresMinPodium: 0,
      nearToUserRegisteredScores: [],

      registeredScoresSize: 5,
      registeredScores: [],
      
      parcipationNb: 0
    }
  }
};
</script>