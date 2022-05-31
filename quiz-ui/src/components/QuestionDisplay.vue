<template>
  <div v-if="question">
    <p>{{ question.title }}</p>
    <img v-if="question.image" :src="question.image" />
    <p>{{ question.text }}</p>
    <div 
      v-for="({ text }, answerId) in question.possibleAnswers" 
      :key="answerId"
    >
      <a @click="onPossibleAnswerClicked(answerId)"> {{ text }} </a>
    </div>
  </div>
</template>

<script>

export default {
  name: "QuestionDisplay",
  props: {
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
  emits: ["answer-selected"],
  methods: {
    onPossibleAnswerClicked(answerId) {
      this.$emit('answer-selected', answerId)
    }
  }
};
</script>