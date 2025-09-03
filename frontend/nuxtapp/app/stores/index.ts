const useManagerStore = defineStore('manager', () => {
  const value: Ref<Manager> = ref({
    login: false, id: '', enterprises: []
  })

  return { value }
})

export {useManagerStore}
