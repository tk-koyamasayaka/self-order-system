import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    categories: [],
    products: [],
    cart: [],
    tableNumber: 1
  },
  getters: {
    cartTotal(state) {
      return state.cart.reduce((total, item) => {
        return total + (item.price * item.quantity)
      }, 0)
    },
    cartItemCount(state) {
      return state.cart.reduce((count, item) => {
        return count + item.quantity
      }, 0)
    }
  },
  mutations: {
    setCategories(state, categories) {
      state.categories = categories
    },
    setProducts(state, products) {
      state.products = products
    },
    addToCart(state, product) {
      const existingItem = state.cart.find(item => item.id === product.id)
      
      if (existingItem) {
        existingItem.quantity++
      } else {
        state.cart.push({
          id: product.id,
          name: product.name,
          price: product.price,
          quantity: 1
        })
      }
    },
    removeFromCart(state, productId) {
      const index = state.cart.findIndex(item => item.id === productId)
      if (index !== -1) {
        state.cart.splice(index, 1)
      }
    },
    updateCartItemQuantity(state, { productId, quantity }) {
      const item = state.cart.find(item => item.id === productId)
      if (item) {
        item.quantity = quantity
      }
    },
    clearCart(state) {
      state.cart = []
    },
    setTableNumber(state, number) {
      state.tableNumber = number
    }
  },
  actions: {
    async fetchCategories({ commit }) {
      try {
        const response = await axios.get('/api/categories/')
        commit('setCategories', response.data)
      } catch (error) {
        console.error('カテゴリの取得に失敗しました', error)
      }
    },
    async fetchProducts({ commit }, categoryId = null) {
      try {
        let url = '/api/products/'
        if (categoryId) {
          url += `?category_id=${categoryId}`
        }
        const response = await axios.get(url)
        commit('setProducts', response.data)
      } catch (error) {
        console.error('商品の取得に失敗しました', error)
      }
    },
    async submitOrder({ commit, state, getters }) {
      try {
        const orderData = {
          table_number: state.tableNumber,
          items: state.cart.map(item => ({
            product_id: item.id,
            quantity: item.quantity
          }))
        }
        
        const response = await axios.post('/api/orders/', orderData)
        commit('clearCart')
        return response.data
      } catch (error) {
        console.error('注文の送信に失敗しました', error)
        throw error
      }
    }
  }
})