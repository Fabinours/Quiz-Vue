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
    this.questions = response.data.questions
    console.log(response.data.questions)
  },
  methods: {
    answerSelected(answerId) {
      this.answers.push(answerId)

      if (this.index == this.questions.length - 1) {
        console.log("end")
      } else {
        this.index++;
      }
    }
  }
};
</script>