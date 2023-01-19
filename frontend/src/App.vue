<script>
import { RouterLink, RouterView } from 'vue-router'
import PageHeader from "@/components/page/PageHeader.vue";

export default {
  components: {PageHeader},
  methods: {

  }
}
</script>

<template>
<div class="wrapper">
  <PageHeader></PageHeader>
  <div class="container">
    <h1 class="mt-5">Hello, vue + bootstrap</h1>
    <h2 class="text-primary">Some text here</h2>
<!--    <button class="btn btn-primary mt-3">Button</button>-->
    <Btn :class="[ 'mt-3' ]">FGHFGH</Btn>
    <div class="row mt-3">
      <div class="col-7">
        <Block>
          <h3>Hello world</h3>
          <Inp label="Login:" name="login"></Inp>
        </Block>
      </div>
    </div>
    <div class="row">
      <div class="col-6">
        <PageSection :title="`Популярные ресурсы`">
          <Block :class="['mb-2']">
            <Link href="https://google.com">Привет</Link>
          </Block>
          <Block :class="['mb-2']">
            <Link href="https://google.com">Привет</Link>
          </Block>
          <Block :class="['mb-2']">
            <Link href="https://google.com">Привет</Link>
          </Block>
        </PageSection>
      </div>
      <div class="col-6"></div>
    </div>

  </div>
</div>
</template>

<style scoped>
</style>
