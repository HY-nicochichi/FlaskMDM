import {accessManagerGet} from '~/composables/ApiClient'
import {setJwt} from '~/composables/JwtManager'
import {useManagerStore} from '~/stores'
import type {Resp} from '~/types'

export default defineNuxtRouteMiddleware(async(to, from) => {
  const manager = useManagerStore()
  const resp: Resp = await accessManagerGet()

  if (resp.status === 200) {
    manager.value = {
      login: true, id: resp.json.id, enterprises: resp.json.enterprises
    }
  }
  else {
    manager.value = {
      login: false, id: '', enterprises: []
    }
    setJwt()
  }

  const NoAuthRoutes: string[] = ['login', 'new_manager']

  if (manager.value.login && NoAuthRoutes.includes(to.name as string)) {
    return navigateTo({name: 'index'})
  }
  if (!manager.value.login && !NoAuthRoutes.includes(to.name as string)) {
    return navigateTo({name: 'login'})
  }
})
