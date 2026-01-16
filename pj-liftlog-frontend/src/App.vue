<template>
  <div id="app">
    <h1>Liftlog Training App</h1>
    <hr />
    <ExerciseList />
   </div> 
</template>

<script setup>
  import ExerciseList from './components/ExerciseList.vue';
  </script>

<style>
  #app {
    font-family: Arial, sans-serif;
    padding: 20px;
    max-width: 600px;
    margin: 0 auto;
  }
</style>