<script setup lang="ts">
  import VueQrcode from 'vue-qrcode'
  import {LoadingSpinner} from '~/components/SvgIcons'
  import {
    accessEnterpriseGet,
    accessEnterpriseDelete,
    accessDevicePatch,
    accessDeviceDelete
  } from '~/composables/ApiClient'
  import type {Enterprise, Device, Resp} from '~/types'

  const enterprise_id: string = useRoute().params.enterprise_id as string ?? ''

  const resp: Resp = await accessEnterpriseGet(enterprise_id)

  if (resp.status !== 200) {
    useRouter().push('/404')
  }

  const enterprise: Enterprise = resp.json

  useHead({title: enterprise.name + ' (' + enterprise_id + ')'})

  const policies = ['default', ...enterprise.policies]

  const deviceModalValues: Ref<Device> = ref({
    id: '',
    model: '',
    serial_number: '',
    policy: ''
  })

  const deleting_enterprise: Ref<boolean> = ref(false)
  const updating_device: Ref<boolean> = ref(false)
  const deleting_device: Ref<boolean> = ref(false)

  function tryOpenDeviceModal(device: Device) {
    deviceModalValues.value.id = device.id
    deviceModalValues.value.model = device.model
    deviceModalValues.value.serial_number = device.serial_number
    deviceModalValues.value.policy = device.policy
  }

  async function tryDeleteEnterprise(): Promise<void> {
    if (confirm('本当に組織を削除しますか？')) {
      deleting_enterprise.value = true
      const resp: Resp = await accessEnterpriseDelete(enterprise_id)
      if (resp.status === 200) {
        useRouter().push({name: 'index'})
      }
      else {
        deleting_enterprise.value = false
      }
    }
  }

  async function tryUpdateDevice(): Promise<void> {
    updating_device.value = true
    const resp: Resp = await accessDevicePatch(
      enterprise_id,
      deviceModalValues.value.id,
      deviceModalValues.value.policy
    )
    if (resp.status === 200) {
      useRouter().go(0)
    }
    else {
      updating_device.value = false
    }
  }

  async function tryDeleteDevice(): Promise<void> {
    if (confirm('本当にデバイスを削除しますか？')) {
      deleting_device.value = true
      const resp: Resp = await accessDeviceDelete(
        enterprise_id, deviceModalValues.value.id
      )
      if (resp.status === 200) {
        useRouter().go(0)
      }
      else {
        deleting_device.value = false
      }
    }
  }
</script>


<template>
  <div class="fs-5 fw-bolder">
    {{ enterprise.name }} ({{ enterprise_id }})
  </div>
  <div class="fs-5 mt-4 fw-bolder">
    エンロールQR (端末でスキャン)<br>
    <vue-qrcode
      class="border border-primary mt-2"
      :value="enterprise.enroll_qrcode" width="300" height="300"
    />
  </div>
  <div class="fs-5 mt-4 fw-bolder">
    端末ポリシー
  </div>
  <div class="ms-3 mt-2" v-for="policy in enterprise.policies">
    <div class="mt-2">
      <NuxtLink :to="'/enterprise/' + enterprise_id + '/policy/edit/' + policy"
        class="text-decoration-none fw-bolder"
      >
        {{ policy }}
      </NuxtLink>   
    </div>
  </div>
  <div class="mt-3 mb-2">
    <NuxtLink :to="'/enterprise/' + enterprise_id + '/policy/new'"
      class="btn btn-primary"
    >
      ＋ 作成
    </NuxtLink>
  </div>
  <div class="fs-5 fw-bolder mt-4">管理中のデバイス</div>
  <div v-for="device in enterprise.devices" class="ms-3 mt-2">
    <div class="mt-2">
      <a class="text-decoration-none fw-bolder"
        data-bs-toggle="modal"
        data-bs-target="#deviceModal"
        @click="tryOpenDeviceModal(device)"
      >
        {{ device.model }} ({{ device.serial_number }})
      </a>
    </div>
  </div>
  
  <div id="deviceModal" class="modal fade" tabindex="-1" aria-labelledby="deviceModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header bg-secondary">
          <h6 class="modal-title text-light fw-bolder" id="deviceModalLabel">
            {{ deviceModalValues.model }} ({{ deviceModalValues.serial_number }})
          </h6>
          <button class="btn-close bg-light" data-bs-dismiss="modal" aria-label="閉じる"></button>
        </div>
        <div class="modal-body" style="background-color:aliceblue">
          <label class="form-label">ポリシー</label>
          <select v-model="deviceModalValues.policy" class="form-select mt-2">
            <option v-for="policy in policies" :value="policy">
              {{ policy }}
              <span v-if="policy === 'default'"> (適用ポリシーなし)</span>
            </option>
          </select>
        </div>
        <div class="modal-footer bg-secondary">
          <button
            class="btn btn-primary me-4"
            @click="tryUpdateDevice" :disabled="updating_device"
          >
            <LoadingSpinner
              v-if="updating_device" :size="'25'" :color="'white'"
            />
            <span v-else>更新</span>
          </button>
          <button
            class="btn btn-danger" data-bs-dismiss="modal"
            @click="tryDeleteDevice" :disabled="deleting_device"
          >
            <LoadingSpinner
              v-if="deleting_device" :size="'25'" :color="'white'"
            />
            <span v-else>削除</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <button
    class="btn btn-danger mt-4"
    @click="tryDeleteEnterprise" :disabled="deleting_enterprise"
  >
    <LoadingSpinner
      v-if="deleting_enterprise" class="mx-3" :size="'25'" :color="'white'"
    />
    <span v-else>組織を削除</span>
  </button>
</template>
