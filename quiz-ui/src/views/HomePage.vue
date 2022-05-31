<template>
  <div>
    <h1>Home page</h1>
    <RouterLink to="/quiz">Démarrer le quiz</RouterLink>

    <h1>{{ registeredScoresSize }} best players!</h1>
    <div v-for="({ playerName, score }, i) in registeredScores" :key="i">
      {{ i + 1 }} / {{ registeredScoresSize }} : {{ playerName }} - {{ score }}
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores : [],
      registeredScoresSize: 5
    }
  },
  async created() {
    const response = await quizApiService.getQuizInfo();
    this.registeredScores = response.data.scores.slice(0, this.registeredScoresSize);
  },
};
</script>