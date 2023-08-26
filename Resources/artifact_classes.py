## Miracle battles


class Artifact:
    def __init__(self, name, img, price, tags, effects):
        self.name = name
        self.img = img
        self.price = price
        self.tags = tags  # List
        self.effects = effects  # List of effects
        self.blocked = 0  # 0 - means unblocked, other number means how many turns needed before artifact could be used


class Artifact_Effect:
    def __init__(self, application, quantity, method, quality, application_tags, other_tags):
        self.application = application
        self.quantity = quantity
        self.method = method
        self.quality = quality
        self.application_tags = application_tags
        self.other_tags = other_tags
