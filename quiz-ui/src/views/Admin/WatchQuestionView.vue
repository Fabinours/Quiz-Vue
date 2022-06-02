<template>
  <div>
    <question-display 
      :question="question" 
      :isAdmin="true"
      @edit-question="editQuestion"
      @delete-question="deleteQuestion"
    />
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
    //Vérification du token administrateur
    if (!participationStorageService.getToken()) {
      //Sinon redirection vers la page de connexion
      this.$router.push("/login");
    }

    //Récupération de la position de la question
    const position = this.$route.params.position;
    this.position = position;

    //Récupération des données de la question
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
    async deleteQuestion() {
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