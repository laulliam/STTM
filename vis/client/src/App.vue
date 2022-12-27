<script setup>
import Map from './components/Map.vue'
</script>

<template>
  <header>
  </header>

  <main id="app">
    <Map />
  </main>
</template>

<style>
  html, body {
    padding: 0;
    margin: 0;
  }
  
  #app {
    position: fixed;
    width: 100%;
    height: 100%;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    background-color: #191a1a;
  }
</style>
