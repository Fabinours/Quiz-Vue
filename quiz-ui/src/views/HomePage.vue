<template>
  <div>
    <h1>Home page</h1>
    <div v-for="({ playerName, score }, i) in registeredScores" :key="i">
      {{ playerName }} - {{ score }}
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores : []
    }
  },
  async created() {
    console.log("Composant Home page 'created'");
    const response = await quizApiService.getQuizInfo();
    this.registeredScores = response.data.scores;
    console.log(this.registeredScores);
  },
};
</script>