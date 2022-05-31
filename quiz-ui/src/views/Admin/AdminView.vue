<template>
  <div>
    <h1>Admin View</h1>
    <router-link to="/admin/question/create">Créer une question</router-link>
    <hr>
    <div>
      <div v-for="({ title, text },i) in questions" :key="i">
        <router-link :to="'/admin/question/watch/' + (i + 1)">{{ title }} - {{ text }}</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "AdminView",
  components: {},
  async created() {
    if (!participationStorageService.getToken()) {
      this.$router.push("/login");
    }

    const response = await quizApiService.getAllQuestions();
    this.questions = response.data.questions;
  },
  data() {
    return {
      questions: []
    }
  }
}
</script>

<style>

</style>