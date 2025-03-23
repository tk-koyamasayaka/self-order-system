<template>
  <div class="menu">
    <h2>メニュー</h2>
    
    <div class="category-tabs">
      <button 
        v-for="category in categories" 
        :key="category.id"
        @click="selectCategory(category.id)"
        :class="['category-tab', { active: selectedCategoryId === category.id }]"
      >
        {{ category.name }}
      </button>
    </div>
    
    <div class="products grid">
      <div v-for="product in products" :key="product.id" class="product-card">
        <div class="product-image" v-if="product.image">
          <img :src="product.image" :alt="product.name">
        </div>
        <div class="product-info">
          <h3>{{ product.name }}</h3>
          <p class="product-description">{{ product.description }}</p>
          <p class="product-price">¥{{ product.price.toLocaleString() }}</p>
          <button @click="addToCart(product)" class="btn btn-primary">カートに追加</button>
        </div>
      </div>
    </div>
    
    <div class="cart-summary" v-if="cartItemCount > 0">
      <p>{{ cartItemCount }}点の商品</p>
      <p>合計: ¥{{ cartTotal.toLocaleString() }}</p>
      <button @click="goToCart" class="btn btn-secondary">カートを見る</button>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'

export default {
  name: 'MenuView',
  data() {
    return {
      selectedCategoryId: null
    }
  },
  computed: {
    ...mapState(['categories', 'products']),
    ...mapGetters(['cartTotal', 'cartItemCount'])
  },
  methods: {
    ...mapMutations(['addToCart']),
    ...mapActions(['fetchCategories', 'fetchProducts']),
    selectCategory(categoryId) {
      this.selectedCategoryId = categoryId
      this.fetchProducts(categoryId)
    },
    goToCart() {
      this.$router.push('/cart')
    }
  },
  async created() {
    await this.fetchCategories()
    if (this.categories.length > 0) {
      this.selectedCategoryId = this.categories[0].id
      await this.fetchProducts(this.selectedCategoryId)
    } else {
      await this.fetchProducts()
    }
  }
}
</script>

<style scoped>
.menu {
  padding: 1rem 0;
}

h2 {
  margin-bottom: 1.5rem;
  text-align: center;
  color: #4a6572;
}

.category-tabs {
  display: flex;
  overflow-x: auto;
  margin-bottom: 2rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #ddd;
}

.category-tab {
  padding: 0.5rem 1rem;
  margin-right: 0.5rem;
  background: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
  font-weight: bold;
  color: #666;
}

.category-tab.active {
  background-color: #f9a826;
  color: white;
}

.product-card {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.product-image {
  height: 150px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  padding: 1rem;
}

.product-info h3 {
  margin-bottom: 0.5rem;
  color: #333;
}

.product-description {
  color: #666;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  height: 40px;
  overflow: hidden;
}

.product-price {
  font-weight: bold;
  color: #f9a826;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.cart-summary {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: white;
  padding: 1rem;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cart-summary p {
  margin: 0;
  font-weight: bold;
}

@media (max-width: 768px) {
  .cart-summary {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>