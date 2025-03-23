<template>
  <div id="app">
    <header class="header">
      <h1>セルフオーダーシステム</h1>
    </header>
    <main class="main">
      <router-view/>
    </main>
    <footer class="footer">
      <p>&copy; 2025 セルフオーダーシステム</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'メイリオ', sans-serif;
  color: #333;
  background-color: #f5f5f5;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  background-color: #4a6572;
  color: white;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.main {
  flex: 1;
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.footer {
  background-color: #4a6572;
  color: white;
  padding: 1rem;
  text-align: center;
  font-size: 0.8rem;
}
</style>