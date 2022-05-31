<template>
  <div>
    <h1>Login page</h1>
    <div id="password-form">
      <p>Saisissez un mot de passe</p>
      <input type="password" placeholder="Mot de passe" v-model="password" />
    </div>
    <button class="btn btn-primary" @click="tryLogin">Ok</button>
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