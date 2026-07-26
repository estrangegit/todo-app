<script setup lang="ts">
import Card from 'primevue/card'
import Button from 'primevue/button'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Message from 'primevue/message'

import { Form, type FormSubmitEvent } from '@primevue/forms'
import { zodResolver } from '@primevue/forms/resolvers/zod'

import { loginSchema } from '@/schemas/auth'
import { login } from '@/api/auth'

const resolver = zodResolver(loginSchema)

const initialValues = {
  username: '',
  password: '',
}

async function onSubmit(event: FormSubmitEvent) {

  if (!event.valid) {
    return
  }

  try {
    const token = await login(event.values.username, event.values.password)
    console.log(token)
  } catch (error) {
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

          <Button type="submit" label="Se connecter" fluid />
        </Form>
      </template>
    </Card>
  </div>
</template>
