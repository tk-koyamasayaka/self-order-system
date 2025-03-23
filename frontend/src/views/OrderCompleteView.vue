<template>
  <div class="order-complete">
    <div class="complete-card">
      <div class="success-icon">✓</div>
      <h2>ご注文ありがとうございます！</h2>
      <p>ご注文を受け付けました。</p>
      <p>しばらくお待ちください。</p>
      
      <div class="actions">
        <button @click="goToHome" class="btn btn-primary">ホームに戻る</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderCompleteView',
  methods: {
    goToHome() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.order-complete {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}

.complete-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  max-width: 500px;
  width: 100%;
  text-align: center;
}

.success-icon {
  width: 80px;
  height: 80px;
  background-color: #4CAF50;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  margin: 0 auto 1.5rem;
}

h2 {
  color: #4a6572;
  margin-bottom: 1rem;
}

p {
  margin-bottom: 0.5rem;
  color: #666;
}

.actions {
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  font-size: 1.1rem;
}
</style>