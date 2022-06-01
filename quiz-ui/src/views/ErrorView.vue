<template>
  <div>
    <center>
      <h1>Erreur</h1>
      <p>
        {{ error }}
      </p>
    </center>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "ErrorView",
  data() {
    return {
      error : ""
    }
  },
  async created() {
    this.error = participationStorageService.getError();
  },
};
</script>