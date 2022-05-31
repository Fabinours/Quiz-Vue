<template>
  <div>
    <h1>Score page</h1>
    <h2>Mon score</h2>
    <p>{{ currentScore }} </p>
    <h2>Classement</h2>
    <div v-for="({ playerName, score }, i) in nearToUserRegisteredScores" :key="i">
      {{ nearToUserRegisteredScoresOffset + i }} / {{ parcipationNb }} : {{ playerName }} - {{ score }}
    </div>
    <h2>Meilleurs scores</h2>
    <div v-for="({ playerName, score }, i) in registeredScores" :key="i">
      {{ i + 1 }} / {{ parcipationNb }} : {{ playerName }} - {{ score }}
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
    
    this.nearToUserRegisteredScoresOffset = index - 1;
    this.nearToUserRegisteredScores = response.data.scores.slice(minIndex, maxIndex);
    this.registeredScores = response.data.scores.slice(0, this.registeredScoresSize);
    this.currentScore = currentScore;
    this.parcipationNb = response.data.scores.length;
  },
  data() {
    return {
      currentScore: 0,

      nearToUserRegisteredScores: [],
      nearToUserRegisteredScoresRange: 2,
      nearToUserRegisteredScoresOffset: 0,

      registeredScores: [],
      registeredScoresSize: 5,
      
      parcipationNb: 0
    }
  }
};
</script>