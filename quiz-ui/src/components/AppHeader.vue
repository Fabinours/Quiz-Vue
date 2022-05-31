<template>
  <header class="border">
    <nav class="navbar navbar-expand-lg navbar-light bg-white">
      <div class="container-fluid">
        <h1 class="h4">Fabiwen Quiz</h1>
        <button
          class="navbar-toggler"
          type="button"
          data-mdb-toggle="collapse"
          data-mdb-target="#navbarExample01"
          aria-controls="navbarExample01"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <i class="fas fa-bars"></i>
        </button>
        <div class="collapse navbar-collapse px-3" id="navbarExample01">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li 
              v-for="({ name, path, requireLogged }, i) in links"
              :key="i"
              class="nav-item"
            >
              <RouterLink class="nav-link" :to="path" v-if="(!requireLogged) || (requireLogged && logged)">
                {{ name }}
              </RouterLink>
            </li>
          </ul>
        </div>
        <button v-if="logged" class="btn btn-primary" @click="logOut">Déconnexion</button>
      </div>
    </nav>
  </header>
</template>

<script>

import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "AppHeader",
  data() {
    return {
      links: [
        {
          name: "Home",
          path: "/",
          requireLogged: false
        },
        {
          name: "About",
          path: "/about",
          requireLogged: false
        },
        {
          name: "Login",
          path: "/login",
          requireLogged: false
        },
        {
          name: "Admin",
          path: "/admin",
          auth: true,
          requireLogged: true
        }
      ]
    };
  },
  computed: {
    logged() {
      return participationStorageService.getToken() != null
    },
  },
  methods: {
    async logOut() {
      await this.$swal.fire(
        'Déconnexion',
        'Vous avez été déconnecté !',
        'success'
      );
      participationStorageService.removeToken();
      this.$router.push("/");
    }
  }
}
</script>

<style>

</style>