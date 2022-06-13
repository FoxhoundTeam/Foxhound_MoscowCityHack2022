module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  devServer: {
    proxy: 'http://51.250.22.246/'
    // proxy: 'http://192.168.107.236:8000/'
  }
}
