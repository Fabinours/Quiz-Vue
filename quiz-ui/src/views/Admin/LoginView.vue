<template>
  <div class="d-flex justify-content-center">
    <div class="card mx-3" style="width: 20rem;">
      <div class="card-body mt-2">
        <h2 class="card-title">Se connecter ? 🙌</h2>
        <div id="password-form">
          <label for="username">Saisissez votre mot de passe</label>
          <input id="username" class="form-control mt-2" type="password" placeholder="Mot de passe" v-model="password" />
        </div>
      </div>
      <div class="card-body d-flex justify-content-center">
        <RouterLink to="/questions">
          <button class="btn btn-primary" @click="tryLogin">
            Se connecter
          </button>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "LoginPage",
  data() {
    return {
      password: ""
    }
  },
  methods: {
    async tryLogin() {

      const response = await quizApiService.login({
        password: this.password
      })

      if (response.status === 401) {
        this.$swal.fire(
          'Mauvais identifiants',
          'Veuillez réessayer',
          'warning'
        )
      } else {

        await this.$swal.fire(
          'Connecté !',
          'Mode administrateur activé',
          'success'
        )

        participationStorageService.saveToken(response.data.token);
        this.$router.push('/admin');
      }

    }
  }
};
</script>