<template>
  <div>
    <question-display
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