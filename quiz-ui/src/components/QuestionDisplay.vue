<template>
  <div class="d-flex justify-content-center flex-wrap">
    <div class="card mx-3" style="width: 30rem;">
      <img v-if="question.image" :src="question.image" class="fill-tag"/>
    </div>

    <div class="card mx-3" style="width: 30rem;" v-if="question">

      <div class="card-body mt-2">
        <h2 class="card-title">{{ question.title }}</h2>
        <p> {{ question.text }} </p>
      </div>

      <ul class="list-group list-group-flush">
        <li 
          class="list-group-item list-group-item-action" 
          v-for="({ text, isCorrect }, answerId) in question.possibleAnswers" 
          :key="answerId"
          @click="onPossibleAnswerClicked(answerId)" :class="isCorrect && isAdmin ? 'text-decoration-underline' : ''"
        >
          {{ text }} 
        </li>
      </ul>
      
      <div v-if="isAdmin" class="card-body d-flex justify-content-around">
        <button class="btn btn-primary" @click="onEditQuestionClicked">Modifier </button>
        <button class="btn btn-danger" @click="onDeleteQuestionClicked">Supprimer</button>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "QuestionDisplay",
  props: {
    isAdmin: {
      type: Boolean,
        required: true,
        default: false
    },
    question: {
      image: {
        type: String,
        required: true,
        default: ""
      },
      position: {
        type: Number,
        required: true,
        default: ""
      },
      text: {
        type: String,
        required: true,
        default: ""
      },
      title: {
        type: String,
        required: true,
        default: ""
      },
      possibleAnswers: {
        type: Array,
        required: true,
        default: () => []
      },
      required: true,
      default: null
    }
  },
  data() {
    return {}
  },
  emits: ["answer-selected", "edit-question", "delete-question"],
  methods: {
    onPossibleAnswerClicked(answerId) {
      this.$emit('answer-selected', answerId)
    },
    onEditQuestionClicked() {
      this.$emit('edit-question')
    },
    onDeleteQuestionClicked() {
      this.$emit('delete-question')
    }
  }
};
</script>

<style scoped>
  .fill-tag {
    width: 100%; height: 100%;
  }
</style>