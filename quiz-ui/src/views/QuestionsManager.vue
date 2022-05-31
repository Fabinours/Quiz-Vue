<template>
  <div>
    <question-display
      :question="questions[index]"
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
    const response = await quizApiService.getAllQuestions();
    this.questions = response.data.questions;
  },
  methods: {
    async answerSelected(answerId) {
      
      this.answers.push(answerId + 1)

      if (this.index == this.questions.length - 1) {
        const results = await quizApiService.createParticipation({
            "playerName": participationStorageService.getPlayerName(),
            "answers": this.answers
        });
        participationStorageService.saveParticipationScore(results.data.score);
        this.$router.push("score")
      } else {
        this.index++;
      }
    }
  }
};
</script>