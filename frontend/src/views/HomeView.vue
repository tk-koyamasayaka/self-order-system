<template>
  <div class="home">
    <div class="welcome-card">
      <h2>ようこそ！</h2>
      <p>セルフオーダーシステムへようこそ。</p>
      <p>テーブル番号を選択して、メニューから注文してください。</p>
      
      <div class="form-group">
        <label class="form-label">テーブル番号</label>
        <select v-model="tableNumber" class="form-input">
          <option v-for="n in 20" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>
      
      <button @click="startOrder" class="btn btn-primary">注文を開始する</button>
    </div>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'HomeView',
  data() {
    return {
      tableNumber: 1
    }
  },
  methods: {
    ...mapMutations(['setTableNumber']),
    startOrder() {
      this.setTableNumber(this.tableNumber)
      this.$router.push('/menu')
    }
  }
}
</script>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}

.welcome-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  max-width: 500px;
  width: 100%;
  text-align: center;
}

h2 {
  color: #f9a826;
  margin-bottom: 1rem;
}

p {
  margin-bottom: 1rem;
  color: #666;
}

.btn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  font-size: 1.1rem;
}
</style>