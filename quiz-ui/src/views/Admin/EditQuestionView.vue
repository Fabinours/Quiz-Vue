<template>
  <div class="d-flex justify-content-center">
    <div class="card mx-3" style="width: 30rem;">
      <div class="card-body mt-2">
        <h2 class="card-title">Editer une question ✨</h2>
        <div id="edit-question-form">
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

          <label class="pt-3">Saisissez l'image</label>
          <input type="file" class="form-control mt-2" accept="image/*" @change="processFile($event)">

          <label for="text" class="pt-3">Saisissez la position de la question dans le quiz</label>
          <input id="position" class="form-control mt-2" type="text" placeholder="Position" v-model="position" />
        </div>
      </div>
      <div class="card-body d-flex justify-content-around">
        <button class="btn btn-primary" @click="updateQuestion">Mettre à jour</button>
        <button class="btn btn-danger" @click="cancelUpdate">Annuler</button>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "UpdateQuestionView",
  components: {},
  async created() {
    //Vérification du token administrateur
    if (!participationStorageService.getToken()) {
      //Sinon redirection vers la page de connexion
      this.$router.push("/login");
    }

    //Récupération de la question à modifier
    const position = this.$route.params.position;
    const response = await quizApiService.getQuestion(position);

    //Autocomplétion des champs avec les données de la bdd
    if (response.status == 200) {
      this.title = response.data.title;
      this.text = response.data.text;
      this.image = response.data.image;
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
      image: "",
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

      // Try update question
      const response = await quizApiService.updateQuestion(this.$route.params.position, {
        position: this.position,
        title: this.title,
        text: this.text,
        image: this.image,
        possibleAnswers: this.possibleAnswers.map((answer, i) => ({
          text: answer,
          isCorrect: this.correctAnswer === i
        })),
      });

      if (response.status == 200) {
        // Question updated
        await this.$swal.fire(
          'Question éditée !',
          'Edition réalisé avec succès',
          'success'
        );
        this.$router.push('/admin');
        return true;
      } else {
        // Question not updated
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
      this.$router.push('/admin/question/watch/' + this.position);
    },
    async processFile(event) {
      // Enregistrement de l'image 
      const file = event.target.files[0];
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
          this.image = reader.result;
          resolve(reader.result);
        }
        reader.onerror = error => reject(error);
      });
    }
  }
}
</script>

<style>

</style>