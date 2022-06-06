<template>
  <div>
    <div v-if="!questions || questions.length == 0" class="d-flex justify-content-center">
      <div class="card mx-3" style="width: 20rem;">
        <div class="card-body">
          <h2 class="card-title">Pas de questions pour le moment...</h2>
        </div>
      </div>
    </div>
    <question-display
      v-else
      :question="questions[index]"
      :isAdmin="false"
      @answer-selected="answerSelected"
    />
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import QuestionDisplay from "@/components/QuestionDisplay.vue";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "QuestionsManager",
  components: {
    QuestionDisplay
  },
  data() {
    return {
      questions: [],
      answers: [],
      index: 0
    }
  },
  async created() {
    //Récupération de la liste de questions
    const response = await quizApiService.getAllQuestions();
    this.questions = response.data.questions;
  },
  methods: {
    async answerSelected(answerId) {
      //Afichage de la bonne réponse

      const Toast = this.$swal.mixin({
        toast: true,
        position: 'top-right',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
      })

      if (this.questions[this.index].possibleAnswers[answerId].isCorrect) {
        await Toast.fire({
          icon: 'success',
          title: 'Cette réponse est correcte 😀'
        })
      } else {
        await Toast.fire({
          icon: 'error',
          title: 'Cette réponse est incorrecte 😅'
        })
      }

      //Enregistrement de la réponse
      this.answers.push(answerId + 1)

      //Si c'est la dernière question, on enregistre la participation sur le serveur
      if (this.index == this.questions.length - 1) {
        const results = await quizApiService.createParticipation({
            "playerName": participationStorageService.getPlayerName(),
            "answers": this.answers
        });
        participationStorageService.saveParticipationScore(results.data.score);
        //Redirection vers la page des résultats
        this.$router.push("score")
      } else {
        this.index++;
      }
    }
  }
};
</script>