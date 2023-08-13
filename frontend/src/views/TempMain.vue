<template>
    <ion-page>
        <h1>Main</h1>

        <div class="cat-image">
            <ion-img style="width: 100%;height: auto;"  src="/media/categories/ART.jpg">
            </ion-img>
        </div>

        
    </ion-page>
    
</template>

<script lang="ts" setup>
import { IonRouterOutlet, IonPage } from '@ionic/vue';
</script>

<style scoped>
.cat-image {
    height: 500px;
    width: 500px;
    margin: 100px;
}
</style>