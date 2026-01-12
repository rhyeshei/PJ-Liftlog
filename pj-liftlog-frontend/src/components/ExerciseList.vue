<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const exercises = ref([]);

onMounted(async () => {
    try {
        // Djangoの ExerciseMasterViewSet (url: /exercises/) を叩く
        const response = await api.get('/exercises/');
        exercises.value = response.data;
    } catch(error){
        console.error('データ取得に失敗しました:', error);
    }
});
</script>

<template>
    <div>
        <h2>トレーニング種目一覧</h2>
        <ul>
            <li v-for="ex in exercises" :key="ex.id">
                {{ ex.name }} ({{ ex.category }})
            </li>
        </ul>
    </div>
</template>
