<script setup>
    import { ref, onMounted } from 'vue';
    import api from '@/services/api';
    
    const exercises = ref([]);
    const newExercise = ref({
      name: '',
      body_part: 'other', // モデルの choices に合わせた初期値
      movement: 'other'
    });
    
    // 一覧取得
    const fetchExercises = async () => {
      try {
        const response = await api.get('exercises/');
        exercises.value = response.data;
      } catch (error) {
        console.error('取得失敗:', error);
      }
    };
    
    // 新規追加
    const addExercise = async () => {
      if (!newExercise.value.name) return;
      try {
        await api.post('exercises/', newExercise.value);
        // フォームをリセット
        newExercise.value.name = '';
        // リストを再取得
        await fetchExercises();
      } catch (error) {
        console.error('追加失敗:', error);
        alert('保存に失敗しました');
      }
    };
    
    onMounted(fetchExercises);
    </script>
    
    <template>
      <div class="exercise-manager">
        <h2>種目マスター</h2>
        
        <div class="add-form">
          <input v-model="newExercise.name" placeholder="種目名（例：ベンチプレス）" />
          <button @click="addExercise">種目を追加</button>
        </div>
    
        <table v-if="exercises.length">
          <thead>
            <tr>
              <th>ID</th>
              <th>種目名</th>
              <th>部位</th>
              <th>動作</th>
            </tr>
          </thead>
          <tbody>
            <li v-for="ex in exercises" :key="ex.id">
              <td>{{ ex.id }}</td>
              <td><strong>{{ ex.name }}</strong></td>
              <td>{{ ex.body_part_label }}</td>
              <td>{{ ex.movement_label }}</td>
            </li>
          </tbody>
        </table>
        <p v-else>種目が登録されていません。</p>
      </div>
    </template>
    
    <style scoped>
    .add-form { margin-bottom: 20px; display: flex; gap: 10px; }
    input { padding: 8px; flex: 1; }
    button { padding: 8px 16px; background-color: #42b983; color: white; border: none; cursor: pointer; }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
    th { background-color: #f4f4f4; }
    </style>