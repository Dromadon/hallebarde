<template>
  <section id="login">
    <h1 class="title">
      Bienvenue sur le partage de fichiers !
    </h1>
    <h2 class="subtitle is-size-6">
      Envoi de fichiers sécurisés permettant de mettre à disposition un lien de
      <br />
      téléchargement pendant 7 jours à vos clients.
    </h2>
    <SignIn />
  </section>
</template>

<script>
import SignIn from "@/components/SignIn";

export default {
  name: "LoginView",
  components: { SignIn }
};
</script>
