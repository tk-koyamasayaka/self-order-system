<template>
  <div class="cart">
    <h2>注文カート</h2>
    
    <div v-if="cart.length === 0" class="empty-cart">
      <p>カートに商品がありません</p>
      <button @click="goToMenu" class="btn btn-primary">メニューに戻る</button>
    </div>
    
    <div v-else>
      <div class="cart-items">
        <div v-for="item in cart" :key="item.id" class="cart-item">
          <div class="item-info">
            <h3>{{ item.name }}</h3>
            <p class="item-price">¥{{ item.price.toLocaleString() }}</p>
          </div>
          
          <div class="item-quantity">
            <button 
              @click="decrementQuantity(item)" 
              class="quantity-btn"
              :disabled="item.quantity <= 1"
            >-</button>
            <span class="quantity">{{ item.quantity }}</span>
            <button 
              @click="incrementQuantity(item)" 
              class="quantity-btn"
            >+</button>
          </div>
          
          <div class="item-subtotal">
            <p>¥{{ (item.price * item.quantity).toLocaleString() }}</p>
          </div>
          
          <button @click="removeItem(item.id)" class="btn-remove">
            <span>×</span>
          </button>
        </div>
      </div>
      
      <div class="cart-summary">
        <div class="summary-row">
          <span>小計:</span>
          <span>¥{{ cartTotal.toLocaleString() }}</span>
        </div>
        <div class="summary-row">
          <span>消費税 (10%):</span>
          <span>¥{{ Math.floor(cartTotal * 0.1).toLocaleString() }}</span>
        </div>
        <div class="summary-row total">
          <span>合計:</span>
          <span>¥{{ Math.floor(cartTotal * 1.1).toLocaleString() }}</span>
        </div>
      </div>
      
      <div class="cart-actions">
        <button @click="goToMenu" class="btn btn-secondary">メニューに戻る</button>
        <button @click="submitOrder" class="btn btn-primary" :disabled="isSubmitting">
          {{ isSubmitting ? '処理中...' : '注文を確定する' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'

export default {
  name: 'CartView',
  data() {
    return {
      isSubmitting: false
    }
  },
  computed: {
    ...mapState(['cart']),
    ...mapGetters(['cartTotal'])
  },
  methods: {
    ...mapMutations(['removeFromCart', 'updateCartItemQuantity']),
    ...mapActions(['submitOrder']),
    goToMenu() {
      this.$router.push('/menu')
    },
    incrementQuantity(item) {
      this.updateCartItemQuantity({
        productId: item.id,
        quantity: item.quantity + 1
      })
    },
    decrementQuantity(item) {
      if (item.quantity > 1) {
        this.updateCartItemQuantity({
          productId: item.id,
          quantity: item.quantity - 1
        })
      }
    },
    removeItem(productId) {
      this.removeFromCart(productId)
    },
    async confirmOrder() {
      this.isSubmitting = true
      try {
        await this.submitOrder()
        this.$router.push('/order-complete')
      } catch (error) {
        alert('注文の処理中にエラーが発生しました。もう一度お試しください。')
      } finally {
        this.isSubmitting = false
      }
    }
  }
}
</script>

<style scoped>
.cart {
  padding: 1rem 0;
  max-width: 800px;
  margin: 0 auto;
}

h2 {
  margin-bottom: 1.5rem;
  text-align: center;
  color: #4a6572;
}

.empty-cart {
  text-align: center;
  padding: 2rem;
}

.empty-cart p {
  margin-bottom: 1rem;
  color: #666;
}

.cart-items {
  margin-bottom: 2rem;
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  background-color: white;
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.item-info {
  flex: 1;
}

.item-info h3 {
  margin: 0;
  color: #333;
}

.item-price {
  color: #666;
  margin: 0;
}

.item-quantity {
  display: flex;
  align-items: center;
  margin: 0 1rem;
}

.quantity-btn {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 1px solid #ddd;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-weight: bold;
}

.quantity-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity {
  margin: 0 0.5rem;
  min-width: 30px;
  text-align: center;
}

.item-subtotal {
  min-width: 100px;
  text-align: right;
  font-weight: bold;
}

.btn-remove {
  background: none;
  border: none;
  color: #e74c3c;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0 0.5rem;
}

.cart-summary {
  background-color: white;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.summary-row.total {
  font-weight: bold;
  font-size: 1.2rem;
  border-top: 1px solid #ddd;
  padding-top: 0.5rem;
  margin-top: 0.5rem;
}

.cart-actions {
  display: flex;
  justify-content: space-between;
}

@media (max-width: 768px) {
  .cart-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .item-info {
    margin-bottom: 0.5rem;
  }
  
  .item-quantity {
    margin: 0.5rem 0;
  }
  
  .item-subtotal {
    text-align: left;
    margin-bottom: 0.5rem;
  }
  
  .btn-remove {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
  }
  
  .cart-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .cart-actions button {
    width: 100%;
  }
}
</style>