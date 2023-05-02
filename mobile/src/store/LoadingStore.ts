import {
  action,
  computed,
  makeAutoObservable,
  makeObservable,
  observable,
} from 'mobx';

export class LoadingStore {
  @observable loadingStatus = 0;

  constructor() {
    makeObservable(this);
  }

  @computed
  get isLoading(): boolean {
    return !!this.loadingStatus;
  }

  @action
  increaseLoadingStatus() {
    this.loadingStatus = this.loadingStatus + 1;
  }

  @action
  decreaseLoadingStatus() {
    if (this.loadingStatus !== 0) {
      this.loadingStatus = this.loadingStatus - 1;
    }
  }
}
