<template>
  <div class="d-flex justify-content-center">
    <div class="card mx-3" style="width: 30rem;">
      <div class="card-body mt-2">
        <h2 class="card-title">Créer une question ✨</h2>
        <div id="create-question-form">
          <label for="title" class="pt-3">Saisissez le titre</label>
          <input id="title" class="form-control mt-2" type="text" placeholder="Titre" v-model="title" />

          <label for="text" class="pt-3">Saisissez le texte</label>
          <input id="text" class="form-control mt-2" type="text" placeholder="Texte" v-model="text" />

          <label class="pt-3">Saisissez les réponses</label>
          <ul class="list-group list-group-flush">
            <li class="list-group-item"  v-for="(answer, i) in possibleAnswers" :key="i">
              <div class="d-flex">
                <input type="radio" :value="i" v-model="correctAnswer" />
                <input class="form-control mx-2" type="text" placeholder="Réponse" v-model="possibleAnswers[i]" />
                <button class="btn btn-danger" @click="removeAnswer(i)">Supprimer</button>
              </div>
            </li>
          </ul>

        </div>
      </div>
      <div class="card-body d-flex justify-content-around">
        <button class="btn btn-primary" @click="addAnswer">Ajouter une réponse</button>
        <button class="btn btn-primary" @click="createQuestion">Créer la question</button>
        <button class="btn btn-danger" @click="cancelUpdate">Annuler</button>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "CreateQuestionView",
  components: {},
  async created() {
    if (!participationStorageService.getToken()) {
      this.$router.push("/login");
    }
  },
  data() {
    return {
      title: "", 
      text: "",
      possibleAnswers: ["", ""],
      correctAnswer: 0
    }
  },
  methods: {
    async createQuestion() {

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
      const response = await quizApiService.createQuestion({
        position: 1,
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
    },
    cancelUpdate() {
      this.$router.push('/admin');
    }
  }
}
</script>

<style>

</style>