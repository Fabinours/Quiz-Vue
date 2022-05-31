<template>
  <div>
    <h1>Edit Question View</h1>
    <div id="create-question-form">

      <p>Saisissez le titre de la question</p>
      <input type="text" placeholder="Titre" v-model="title" />

      <p>Saisissez le texte de la question</p>
      <input type="text" placeholder="Texte" v-model="text" />

      <p>Saisissez les réponses de la question</p>

      <div v-for="(answer, i) in possibleAnswers" :key="i">
        <input type="text" placeholder="Réponse" v-model="possibleAnswers[i]" />
        <input type="radio" :value="i" v-model="correctAnswer" />
        <button @click="removeAnswer(i)">Supprimer</button>
      </div>

      <button @click="addAnswer()">Ajouter</button>

    </div>
    <button class="btn btn-primary" @click="updateQuestion">Mettre à jour la question</button>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "UpdateQuestionView",
  components: {},
  async created() {
    if (!participationStorageService.getToken()) {
      this.$router.push("/login");
    }

    const position = this.$route.params.position;
    const response = await quizApiService.getQuestion(position);

    if (response.status == 200) {
      this.title = response.data.title;
      this.text = response.data.text;
      this.possibleAnswers = response.data.possibleAnswers.map(({ text }) => text);
      this.correctAnswer = response.data.possibleAnswers.findIndex(({ isCorrect }) => isCorrect);
    }

    this.position = parseInt(position);
  },
  data() {
    return {
      position: 0,
      title: "",
      text: "",
      possibleAnswers: ["", ""],
      correctAnswer: 0
    }
  },
  methods: {
    async updateQuestion() {

      // Valid form
      if (!this.title) {
        this.$swal.fire(
          'Formulaire invalide',
          'Veuillez saisir un titre',
          'error'
        )
        return false;
      }

      if (!this.text) {
        this.$swal.fire(
          'Formulaire invalide',
          'Veuillez saisir un texte',
          'error'
        )
        return false;
      }

      if (this.possibleAnswers.some(answer => !answer)) {
        this.$swal.fire(
          'Formulaire invalide',
          'Veuillez saisir toutes les réponses',
          'error'
        )
        return false;
      }
      
      // Try create question
      const response = await quizApiService.updateQuestion(this.$route.params.position, {
        position: this.position,
        title: this.title,
        text: this.text,
        image: "",
        possibleAnswers: this.possibleAnswers.map((answer, i) => ({
          text: answer,
          isCorrect: this.correctAnswer === i
        })),
      });

      if (response.status == 200) {
        // Question created
        await this.$swal.fire(
          'Question crée !',
          'Ajout réalisé avec succès',
          'success'
        );
        this.$router.push('/admin');
        return true;
      } else {
        // Question not created
        this.$swal.fire(
          'Un problème est survenu',
          'Veuillez réessayer plus tard',
          'warning'
        );
        return false;
      }
    },
    removeAnswer(i) {
      if (this.possibleAnswers.length == 2)
        return ;

      if (this.possibleAnswers.length - 1 == i) 
        this.correctAnswer = 0
      
      this.possibleAnswers.splice(i, 1);
    },
    addAnswer() {
      this.possibleAnswers.push("");
    }
  }
}
</script>

<style>

</style>