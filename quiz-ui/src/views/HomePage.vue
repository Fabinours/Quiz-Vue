<template>
  <div class="d-flex justify-content-center">
    <div class="card mx-3" style="width: 20rem;">
      <div class="card-body">
        <h2 class="card-title">Jouer 😊</h2>
        <p class="card-text">
          Les règles du jeu sont simples : répondez juste aux différentes questions afin de remporter un maximum de points ! 
          NB : Chaque réponse à une unique bonne réponse.
        </p>
      </div>

      <div class="card-body d-flex justify-content-center">
        <RouterLink to="/quiz">
          <button class="btn btn-primary">
            Démarrer le quiz
          </button>
        </RouterLink>
      </div>
    </div>

    <div class="card mx-3" style="width: 20rem;">
      <div class="card-body">
        <h2 class="card-title">Meilleurs scores 👌</h2>
        <p class="card-text">Jouez et obtenez le meilleur score possible afin de figurer parmis les meilleurs joueurs du site !</p>
      </div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item" v-for="({ playerName, score }, i) in registeredScores" :key="i">
          {{ i + 1 }}/{{ registeredScoresSize }} : {{ playerName }} avec {{ score }} points !
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
//import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores : [],
      registeredScoresSize: 5
    }
  },
  async created() {
    //Meilleurs scores
    const response = await quizApiService.getQuizInfo();
    this.registeredScores = response.data.scores.slice(0, this.registeredScoresSize);
  },
};
</script>