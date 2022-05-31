<template>
  <div>
    <h1>Watch Question View</h1>
    <div>

      <question-display :question="question" :isAdmin="true"/>

    </div>
    <button class="btn btn-primary" @click="editQuestion">Modifier</button>
    <button class="btn btn-danger" @click="removeQuestion">Supprimer</button>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";
import QuestionDisplay from "@/components/QuestionDisplay.vue";

export default {
  name: "WatchQuestionView",
  components: { QuestionDisplay },
  async created() {
    if (!participationStorageService.getToken()) {
      this.$router.push("/login");
    }

    const position = this.$route.params.position;
    this.position = 1;

    const response = await quizApiService.getQuestion(position);
    this.question = response.data;
  },
  data() {
    return {
      position: 0,
      question: {
        title: "",
        text: "",
        possibleAnswers: [],
        correctAnswer: 0
      }
    }
  },
  methods: {
    editQuestion() {
      this.$router.push(`/admin/question/edit/${this.position}`);
    },
    async removeQuestion() {
      const response = await quizApiService.deleteQuestion(this.position);

      if (response.status === 204) {

        this.$swal.fire({
          title: "Question supprimée",
          text: "La question a bien été supprimée",
          icon: "success"
        });
        this.$router.push("/admin");
      } else {
        this.$swal.fire({
          title: "Erreur",
          text: "Une erreur est survenue lors de la suppression de la question",
          icon: "error"
        });
      }
    },
  }
}
</script>

<style>

</style>