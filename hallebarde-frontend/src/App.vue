<template>
  <div id="app">
    <section class="hero is-fullheight">
      <div class="hero-body">
        <div class="container has-text-centered">
          <figure class="image container is-128x128">
            <img
              src="https://www.octo.com/wp-content/themes/octo-v1/img/logo-mini-color.svg"
            />
          </figure>
          <LoginView />
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import LoginView from "./components/LoginView.vue";

export default {
  name: "App",
  components: { LoginView }
};
</script>

<style lang="sass">
@import '@/design/index.sass'
</style>
