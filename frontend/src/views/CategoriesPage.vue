<template>
  <ion-page>
    <ion-content class="ion-padding">
      
      <p class="page-heading">Explore Your Interests</p>

      <div class="grid-container">

				<div
					class="grid-item cpointer"
					v-for="(cat, index) in category.categories"
					:key="index"
					@click="openCategory(cat)"
				>

					<ion-img class="cat-image" :src="`/media/${cat.image}`">
					</ion-img>

					<div class="cat-title">
						{{cat.name}}
					</div>

					<div class="cat-description" :title="cat.description">
						{{cat.description}}
					</div>

				</div>

      </div>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { useCategoryStore } from '@/stores/category';
import { IonPage, IonContent, IonImg, IonCol, IonGrid, IonRow, IonCard, IonCardContent, useIonRouter  } from '@ionic/vue';
import { categoryObject } from '@/mixims/interfaces'
import { scrollTop } from '@/composables/scroll'

scrollTop()

const ionRouter = useIonRouter();
const category = useCategoryStore();

category.getCategories()

function openCategory (category: categoryObject) {
  ionRouter.push(`interests/${category.id}/posts`)
}
</script>

<style scoped>
.page-heading {
  margin: 0px;
  font-size: 23px;
  font-weight: 500;
  margin-bottom: 10px;
  margin-left: 5px;
	color: var(--ion-color-dark-tint);
}
.grid-container {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
	grid-gap: 20px;
	/* Ensure all rows have the same height */
	grid-auto-rows: auto;
	padding: 5px;
}
.grid-item {
  border: 1px solid var(--ion-color-light-shade);
	color: var(--ion-text-color);
	border-radius: 10px;
	padding: 20px;
	display: flex;
	flex-direction: column;
	text-align: center;
	background: var(--ion-card-background);
}
.grid-item:hover {
  box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px, rgba(17, 17, 26, 0.05) 0px 8px 32px;
}
.cat-image::part(image) {
  max-width: 100%;
	max-height: 220px;
  object-fit: cover;
	border-radius: 5px;
}
.cat-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--ion-color-dark-tint);
	line-height: 2;
	padding-top: 5px;
}
@media only screen and (max-width: 992px) {
  .cat-title  {
    font-size: 15px;
  }
  .cat-description {
    font-size: 12.5px;
  }
}
@media only screen and (max-width: 576px) {
	.grid-container {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
		padding: 0px;
		grid-gap: 15px;;
	}
	.grid-item {
		padding: 17px;
	}
}
</style>