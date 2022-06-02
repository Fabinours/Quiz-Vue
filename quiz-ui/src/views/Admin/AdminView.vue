<template>
  <div class="d-flex justify-content-center">
    <div class="card mx-3" style="width: 40rem;">
      <div class="card-body">
        <h2 class="card-title">Toutes les questions... 😊</h2>
      </div>

      <ul class="list-group list-group-flush">
        <li class="list-group-item list-group-item-action" v-for="({ title, text },i) in questions" :key="i" @click="onQuestionClicked(i)">
          {{ title }} - {{ text }}
        </li>
      </ul>

      <div class="card-body d-flex justify-content-center">
        <router-link to="/admin/question/create">
          <button class="btn btn-primary">
            Créer une question
          </button>
        </router-link>
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
    //Vérification du token administrateur
    if (!participationStorageService.getToken()) {
      //Sinon redirection vers la page de connexion
      this.$router.push("/login");
    }

    //Récupération des questions
    const response = await quizApiService.getAllQuestions();
    this.questions = response.data.questions;
  },
  data() {
    return {
      questions: []
    }
  },
  methods: {
    onQuestionClicked(i) {
      this.$router.push("/admin/question/watch/" + (i + 1));
    }
  }
}
</script>

<style>

</style>