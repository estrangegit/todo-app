<script setup lang="ts">
import Button from 'primevue/button'
import Card from 'primevue/card'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Password from 'primevue/password'

import { Form, type FormSubmitEvent } from '@primevue/forms'
import { zodResolver } from '@primevue/forms/resolvers/zod'

import { ApiError } from '@/errors/api.errors'
import router from '@/router'
import { loginSchema } from '@/schemas/auth'
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'

const resolver = zodResolver(loginSchema)
const authStore = useAuthStore()

const initialValues = {
  username: '',
  password: '',
}

const authenticationError = ref('')

async function onSubmit(event: FormSubmitEvent) {
  if (!event.valid) {
    return
  }

  try {
    await authStore.login(event.values.username, event.values.password)
    await router.push('/')
  } catch (error) {
    if (error instanceof ApiError) {
      authenticationError.value = error.message
      return
    }

    console.error(error)
  }
}
</script>

<template>
  <div class="flex justify-content-center align-items-center min-h-screen">
    <Card class="w-full md:w-8 lg:w-3">
      <template #title> Connexion </template>

      <template #content>
        <Form
          v-slot="$form"
          :resolver="resolver"
          :initialValues="initialValues"
          @submit="onSubmit"
          class="flex flex-column gap-4"
        >
          <div class="flex flex-column gap-1">
            <FloatLabel variant="on">
              <InputText name="username" fluid :invalid="$form.username?.invalid" />
              <label for="username"> Nom d'utilisateur </label>
            </FloatLabel>

            <Message v-if="$form.username?.invalid" severity="error" size="small" variant="simple">
              {{ $form.username.error?.message }}
            </Message>
          </div>

          <div class="flex flex-column gap-1">
            <FloatLabel variant="on">
              <Password
                name="password"
                :feedback="false"
                toggle-mask
                fluid
                :invalid="$form.password?.invalid"
              />
              <label for="password"> Mot de passe </label>
            </FloatLabel>

            <Message v-if="$form.password?.invalid" severity="error" size="small" variant="simple">
              {{ $form.password.error?.message }}
            </Message>
          </div>
          <Message
            v-if="authenticationError"
            severity="error"
            size="small"
            variant="simple"
            class="mb-3"
            >{{ authenticationError }}</Message
          >
          <Button type="submit" label="Se connecter" fluid />
        </Form>
      </template>
    </Card>
  </div>
</template>
